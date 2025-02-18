from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

users = {}
posts = []
post_id_counter = 1 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_users')
def view_users():
    return jsonify(users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        users[username] = username
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/view_posts')
def view_posts():
    return jsonify(posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    global post_id_counter
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username']

        if username not in users:
            users[username] = username

        post = {
            'id': post_id_counter,
            'title': title,
            'content': content,
            'username': username
        }
        posts.append(post)
        post_id_counter += 1

        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('index'))

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        return redirect(url_for('index'))

    return render_template('edit_post.html', post=post)

@app.route('/manage_posts')
def manage_posts():
    return render_template('manage_posts.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)