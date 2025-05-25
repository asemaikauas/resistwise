from flask import Blueprint, render_template_string
from flask import render_template, request, flash, redirect, url_for 
from flask_login import login_required, current_user


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('signup.html')

@main.route('/dashboard') 
@login_required 
def dashboard():
    return render_template('dashboard.html') 


@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@main.route('/patients')
@login_required
def patients():
    return render_template('patients.html')

@main.route('/history')
@login_required
def history():
    return render_template('history.html')

from flask import Flask, render_template, request

@main.route('/info')
def info():
    # Получаем параметры из URL
    patient_name = request.args.get('name', 'Неизвестный пациент')
    probability = request.args.get('probability', '0')
    antibiotic = request.args.get('antibiotic', 'Не назначен')
    result = request.args.get('result', 'Отсутствует')
    
    return render_template('info.html', 
                         patient_name=patient_name,
                         probability=probability,
                         antibiotic=antibiotic,
                         result=result)


