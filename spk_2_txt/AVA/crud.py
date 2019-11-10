from flask import Blueprint, current_app, redirect, render_template, request, url_for
from AVA import model, storage, voices
crud = Blueprint('crud', __name__)


# [START upload audio file]
def upload_file(file):
    """
    Upload the user audio file to the GCloud Storage
    :param file: Audio file
    :return: GCloud Storage public URL
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s",file.filename, public_url
    )
    return public_url
# [END upload_image_file]


@crud.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":

        data = request.form.to_dict(flat=True)

        audio = upload_file(request.files.get('audio'))

        if audio:
            data['audioUrl'] = audio
        data['textUrl'] = "Awaiting Transcription"
        audio_data = model.create(data)


        return redirect(url_for(".list"))
    return render_template("add.html", action="Add", file={})


@crud.route("/list")
def list():
    token = request.args.get('page_token',None)
    if token:
        token = token.encode('utf-8')

    files, next_page_token = model.list(cursor=token)

    return render_template('uploads.html', Files=files, next_page_token=next_page_token)

@crud.route("/convert")
def convert():
    """
    converts all uploaded audio to text files
    :return: the uploads page where the text files should be now
    """

    files, _ = model.list()
    #return render_template("display.html", Files=files)
    for file in files:
        filename = file['title'] + "transcription.txt"
        transcript = voices.sample_recognition(file['audioUrl'])
        content_type = 'application/json'
        file['textUrl'] = storage.upload_file(transcript, filename, content_type)
        model.update(file, id=file['id'])
    return redirect(url_for(".list"))

@crud.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        files, _ = model.list()
        for file in files:
            model.delete(file['id'])
        return redirect(url_for(".list"))

    return render_template("delete.html", action='Delete')
