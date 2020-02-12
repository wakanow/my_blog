from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional, URL, Length


class CommentForm(FlaskForm):
    author = StringField('名字', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('提交')