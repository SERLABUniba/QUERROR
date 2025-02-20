from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
total_pages = 10


@app.route('/', methods=['GET'])
def index():
    # Get the page number from the query string, default to 1 if not provided
    page = int(request.args.get('page', 1))
    print(f"Page value GET received: {page}")

    # Your pagination logic and template rendering here
    return render_template('index.html', page=page, total_pages=total_pages)


@app.route('/test', methods=['POST'])
def test():
    # Get the page number from the form data, default to 1 if not provided
    page = int(request.form.get('page', 1))
    print(f"Page value POST received: {page}")
    # Handle form submission, redirect to the next page
    # Here you can process the form data and redirect as needed
    return redirect(url_for('next_page', page=page))


@app.route('/next_page/<int:page>')
def next_page(page):
    # Render the next_page template and pass the page number
    return render_template('next_page.html', page=page)


if __name__ == '__main__':
    app.run(debug=True)
