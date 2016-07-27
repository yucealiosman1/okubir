# -*- coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_login import current_user, login_required
from wtforms import PasswordField
from flask_security import utils
from okubir.models import *
from okubir import app, dao
from okubir.forms import RecommendBookForm
from flask import redirect, url_for, render_template, request, session, flash

class CommonView(ModelView):
    create_modal = True
    edit_modal = True
    
    def is_accessible(self):
        return current_user.has_role('admin')

@app.route('/recommend_book', methods=['POST', 'GET'])
@login_required
def recommendBook():
    if 'admin' not in current_user.roles or not session['ids_list']:
        flash(u'Bu sayfaya erişim izniniz yok.', 'warning')
        return redirect(url_for('index'))
    form = RecommendBookForm(request.form)
    if form.validate_on_submit():
        ids = session['ids_list']
        for user_id in ids:
            dao.associateBookWithUser(form.book.data, user_id, Status.recommended)
        dao.commit()
        #session['ids_list'] = None
        flash(u'Kitap önerme tamamlandı.', 'info')
    return render_template('recommend_book.html', form=form)

class UserView(CommonView):
    column_exclude_list = ['password',]
    form_excluded_columns = ['password','book_assocs', 'reading_goal']
    column_searchable_list = ['name', 'surname']
    column_editable_list = ['confirmed']
    column_list = ['email', 'name', 'surname', 'last_login', 'confirmed_at', 'confirmed', 'birth_date', 'il', 'ilce', 'semt','interests']
    column_filters = ['interests']
    
    @action('recommend', 'Kitap oner', 'Bu kullanicilara kitap onermek istediginize emin misiniz?')
    def action_approve(self, ids):
        #users = User.query.filter(User.id.in_(ids)).all()
        session['ids_list'] = ids
        return redirect(url_for('recommendBook'))
            
    def scaffold_form(self):
        form_class = super(UserView, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class
    
    def on_model_change(self, form, model, is_created):
        if hasattr(model, 'password2') and len(model.password2):
            model.password = utils.encrypt_password(model.password2)

class BookView(CommonView):
    form_excluded_columns = ['user_assocs']
    column_list = ['publisher', 'author', 'name', 'publication_place', 'publication_year', 'isbn', 'page_amount', 'ebook_fname', 'categories']
    
class PublisherView(CommonView):
    column_list = ['name', 'books']
    form_excluded_columns = ['books']
    
class SummaryView(CommonView):
    column_list = ['book', 'user']
    column_searchable_list = ['userbook.book.name', 'userbook.user.name']

class AuthorView(CommonView):
    column_list = ['name', 'surname', 'books']
    form_excluded_columns = ['books']
    
