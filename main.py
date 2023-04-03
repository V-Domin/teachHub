from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, URLField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esl_plans.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app)

with app.app_context():
    class Lesson(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), nullable=False)
        sub_title = db.Column(db.String(250), nullable=False)
        tag_level = db.Column(db.String(250), nullable=False)
        tag_field = db.Column(db.String(250), nullable=False)
        tag_1 = db.Column(db.String(250))
        tag_2 = db.Column(db.String(250))
        tag_3 = db.Column(db.String(250))
        tag_4 = db.Column(db.String(250))
        body = db.Column(db.Text, nullable=False)
        date = db.Column(db.String(250), nullable=False)
        img_url = db.Column(db.String(250), nullable=False)
        img_url_full = db.Column(db.String(250), nullable=False)
        video_url = db.Column(db.String(250), nullable=False)
        student_v = db.Column(db.String(250), nullable=False)
        teacher_v = db.Column(db.String(250), nullable=False)
        presentation = db.Column(db.String(250), nullable=False)

    # db.create_all()
    # new_lesson = Lesson(
    #     title = 'Towards a car-free future',
    #     sub_title = 'In this lesson about passive voice, students practise using passive voice. They also watch a video and discuss different types of crime.',
    #     tag_level = 'A2',
    #     tag_field = 'Grammar',
    #     tag_1 = 'Global Issue',
    #     tag_2='City',
    #     tag_3='Environment',
    #     body = 'This flipped lesson focuses on a grammar topic of double comparatives and a discussion about car-free cities. Students watch a video and work with grammar on their own. In the lesson, they have more speaking practice and creative work.',
    #     date = '09.03.2023',
    #     video_url = 'sCSkNiyYv8g',
    #     img_url = 'https://images.unsplash.com/photo-1677272472658-08a9d1b1b7ee?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80',
    #     img_url_full = 'https://images.unsplash.com/photo-1601324024252-d2ca364fef25?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=435&q=80',
    #     student_v = 'https://eslbrains.com/wp-content/uploads/unlimited/ESL-Brains-How-to-be-happy-SV-2287.pdf',
    #     teacher_v = 'https://eslbrains.com/wp-content/uploads/unlimited/ESL-Brains-How-to-be-happy-TV-2287.pdf',
    #     presentation = 'https://docs.google.com/presentation/d/1fo07krHLA9N2hI4c4Jh30jt4OqvMyYGIqBhCLjC5Ldo/edit'
    # )
    # db.session.add(new_lesson)
    # db.session.commit()

class LessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    sub_title = StringField('Short Description', validators=[DataRequired()])
    tag_level = SelectField('Level', validators=[DataRequired()], choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'),
                                                                           ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')])
    tag_field = SelectField('Field', validators=[DataRequired()], choices=[('Grammar', 'Grammar'), ('Vocabulary', 'Vocabulary'),
                                                                           ('Speaking', 'Speaking'), ('Reading', 'Reading')])
    tag_1 = StringField('Tag 1')
    tag_2 = StringField('Tag 2')
    tag_3 = StringField('Tag 3')
    tag_4 = StringField('Tag 4')
    body = CKEditorField('Description', validators=[DataRequired()])
    # date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    img_url = StringField('Image Preview URL (450x300)', validators=[DataRequired(), URL()])
    img_url_full = StringField('Main Image URL (600x700)', validators=[DataRequired(), URL()])
    video_url = StringField('Video ID')
    student_v = StringField('Student Worksheet URL', validators=[DataRequired(), URL()])
    teacher_v = StringField('Teacher Worksheet URL', validators=[DataRequired(), URL()])
    presentation = StringField('Presentation URL', validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Lesson")


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/lessons")
def all_lessons():
    lessons = Lesson.query.all()
    return render_template('main.html', lessons=lessons)

@app.route("/lesson/<int:id>")
def lesson(id):
    requested_lesson = Lesson.query.get(id)
    return render_template('lesson.html', lesson=requested_lesson)

@app.route("/add", methods=['GET', 'POST'])
def add():
    global date
    form = LessonForm()

    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        tag_level = form.tag_level.data
        tag_field = form.tag_field.data
        tag_1 = form.tag_1.data
        tag_2 = form.tag_2.data
        tag_3 = form.tag_3.data
        tag_4 = form.tag_4.data
        body = form.body.data
        date = date.today().strftime("%B %d, %Y")
        img_url = form.img_url.data
        img_url_full = form.img_url_full.data
        video_url = form.video_url.data
        student_v = form.student_v.data
        teacher_v = form.teacher_v.data
        presentation = form.presentation.data

        new_lesson = Lesson(
        title = title,
        sub_title = sub_title,
        tag_level = tag_level,
        tag_field = tag_field,
        tag_1 = tag_1,
        tag_2= tag_2,
        tag_3=tag_3,
        tag_4 = tag_4,
        body = body,
        date = date,
        video_url = video_url,
        img_url = img_url,
        img_url_full = img_url_full,
        student_v = student_v,
        teacher_v = teacher_v,
        presentation = presentation,
        )

        db.session.add(new_lesson)
        db.session.commit()
        return redirect(url_for('all_lessons'))

    return render_template('add.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    requested_lesson = Lesson.query.get(id)
    form = LessonForm(obj=requested_lesson)
    if form.validate_on_submit():
        requested_lesson.title = form.title.data
        requested_lesson.sub_title = form.sub_title.data
        requested_lesson.tag_level = form.tag_level.data
        requested_lesson.tag_field = form.tag_field.data
        requested_lesson.tag_1 = form.tag_1.data
        requested_lesson.tag_2 = form.tag_2.data
        requested_lesson.tag_3 = form.tag_3.data
        requested_lesson.tag_4 = form.tag_4.data
        requested_lesson.body = form.body.data
        requested_lesson.img_url = form.img_url.data
        requested_lesson.img_url_full = form.img_url_full.data
        requested_lesson.video_url = form.video_url.data
        requested_lesson.student_v = form.student_v.data
        requested_lesson.teacher_v = form.teacher_v.data
        requested_lesson.presentation = form.presentation.data

        db.session.commit()
        return redirect(url_for('lesson', id=id))
    return render_template('add.html', form=form)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    requested_lesson = Lesson.query.get(id)
    db.session.delete(requested_lesson)
    db.session.commit()
    return redirect(url_for('all_lessons'))

if __name__ == "__main__":
    app.run(debug=True)