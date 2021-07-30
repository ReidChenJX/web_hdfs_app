#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time     : 2021/7/27 10:24
# @Author   : ReidChen
# Document  ：定义登录页，展示页的表格结构

from .db_table import UserTable
from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email


class LoginForm(Form):
    username = StringField(label='登录名:',
                           validators=[
                               DataRequired('此字段不能为空'),
                               length(6, 64, '长度必须在6-64之间')
                           ])
    password = PasswordField(label='密码:',
                             validators=[
                                 DataRequired(),
                                 length(6, 128, '长度必须在6-18之间'),
                                 Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                        '密码只包含字母数字下划线')
                             ])
    remember_me = BooleanField('是否记住密码?', default=False)
    submit = SubmitField('登录')
    
    def validate_user(self, field):
        user = UserTable.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('账户未注册')


class RegisterForm(Form):
    username = StringField(
        label='用户名:',
        validators=[
            DataRequired('用户名不能为空'),
            length(2, 18, '长度必须在6-18之间')
            #  Regexp('^[A-Za-z][A-Za-z0-9_.]$', 0, "用户名只允许字母数字下划线")
        ])
    # email = StringField(label='电子邮箱:',
    #                     validators=[
    #                         DataRequired('此字段不能为空'),
    #                         length(6, 64, '长度必须在6-64之间'),
    #                         Email('邮箱格式有误')
    #                     ])
    password = PasswordField(label='密码:',
                             validators=[
                                 DataRequired('此字段不能为空'),
                                 length(3, 128, '长度必须在6-18之间'),
                                 Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                        '密码只包含字母数字下划线')
                             ])
    password_again = PasswordField(label='再次输入密码:',
                                   validators=[
                                       DataRequired('此字段不能为空'),
                                       length(3, 128, '长度必须在6-18之间'),
                                       Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                              '密码只包含字母数字下划线'),
                                       EqualTo('password', message='密码不一致')
                                   ])
    #  verification_code = StringField('验证码', validators=[
    #  DataRequired('此字段不能为空'),
    #  length(4,4,'填写4位验证码'),
    #  ])
    # about_me = TextAreaField(label='关于我:')
    #  about_me= TextAreaField(label='关于我:', validators = [
    #  length(6,128,'长度必须在6-18之间')])
    submit = SubmitField("注册")
    
    def validate_user(self, field):
        if UserTable.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已被注册')


class ResetPassword(Form):
    old_password = PasswordField(label='输入旧密码:',
                                 validators=[
                                     DataRequired('此字段不能为空'),
                                     length(6, 128, '长度必须在6-18之间'),
                                     Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                            '密码只包含字母数字下划线'),
                                 ])
    new_password = PasswordField(label='输入新密码:',
                                 validators=[
                                     DataRequired('此字段不能为空'),
                                     length(6, 128, '长度必须在6-18之间'),
                                     Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                            '密码只包含字母数字下划线'),
                                 ])
    new_password_again = PasswordField(label='再次输入密码:',
                                       validators=[
                                           DataRequired('此字段不能为空'),
                                           length(6, 128, '长度必须在6-18之间'),
                                           Regexp(
                                               r'^[a-zA-Z0-9_][a-zA-Z0-9]*$',
                                               0, '密码只包含字母数字下划线'),
                                           EqualTo('new_password',
                                                   message='密码不一致')
                                       ])
    submit = SubmitField("更新密码")
