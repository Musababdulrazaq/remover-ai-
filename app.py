from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # دڵنیابوونەوە لەوەی وێنە بارکراوە
    if 'image' not in request.files:
        return "هیچ وێنەیەک نەبارکراوە", 400

    file = request.files['image']
    if file.filename == '':
        return "هیچ وێنەیەک نەدیاریکراوە", 400

    # کارکردن لەسەر وێنەکە کە بارکراوە
    input_image = file.read()
    output_image = remove(input_image)
    img = Image.open(io.BytesIO(output_image)).convert("RGBA")

    # پاشەکەوتکردنی وێنەکە بۆ ئەکستراککردن بۆ بەکارهێنەر
    output_io = io.BytesIO()
    img.save(output_io, "PNG")
    output_io.seek(0)

    # ناردنی وێنەی وەرگرتەوە بۆ بەکارهێنەر
    return send_file(output_io, mimetype="image/png", as_attachment=True, download_name="output.png")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

