from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

blog_posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
]

# Save the list to 'data.json'
with open('data.json', 'w') as json_file:
    json.dump(blog_posts, json_file, indent=4)


@app.route('/')
def index():
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('name')
        title = request.form.get('title')
        content = request.form.get('content')

        # Append the new post to the list
        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)

        # Save the updated list back to the JSON file
        with open('data.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global blog_posts
    new_posts = []
    for post in blog_posts:
        if post['id'] != post_id:
            new_posts.append(post)
    blog_posts = new_posts

    with open('data.json', 'w') as json_file:
        json.dump(blog_posts, json_file, indent=4)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    with open('data.json', 'r') as json_file:
        blog_posts = json.load(json_file)

    post = None
    for p in blog_posts:
        if p['id'] == post_id:
            post = p
            break

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get the updated form data from the user
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated blog_posts list back to the data.json file
        with open('data.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=4)

        # Redirect back to the index page after updating
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
