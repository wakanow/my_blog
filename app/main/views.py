from . import main
from flask import render_template, request, redirect, current_app, \
    abort, make_response, flash, url_for
from app.models import Post, Comment, Category
from flask_login import current_user
from app.utils import redirect_back
from app.main.forms import CommentForm
from app.extensions import db


@main.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['BLUELOG_POST_PER_PAGE']
        pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
        posts = pagination.items
        # user = User.query.get(int(current_user.id))
        return render_template('index.html', posts=posts, pagination=pagination)
    else:
        return render_template('index.html')


@main.route('/show_post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    form = CommentForm()
    if current_user.is_authenticated:
        form.author.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, body=body, post=post)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        db.session.add(comment)
        print('---comment-------',comment.body)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论已经发表', 'success')
        print(post_id)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)



@main.route('/show_category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', posts=posts, pagination=pagination, category=category)


@main.route('/reply_comment<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('不能评论', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@main.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response



@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/new_post')
def new_post():
    return ''