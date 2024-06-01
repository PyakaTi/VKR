from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User, Document, AnalysisResult, SortingResult
import nltk

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # Пример обработки файла и добавления его в базу данных
        document = Document(content=file.read().decode('utf-8'), status='uploaded')
        db.session.add(document)
        db.session.commit()
        # Запуск анализа и сортировки документа
        analyze_and_sort_document(document.id)
        return redirect(url_for('index'))
    return render_template('upload.html', title='Upload Document')

@app.route('/results/<int:document_id>')
def results(document_id):
    document = Document.query.get(document_id)
    analysis_results = document.analysis_results.all()
    sorting_results = document.sorting_results.all()
    return render_template('results.html', document=document, analysis_results=analysis_results, sorting_results=sorting_results)

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Settings')

def analyze_and_sort_document(document_id):
    document = Document.query.get(document_id)
    content = document.content

    # Анализ документа (пример с использованием NLTK)
    words = nltk.word_tokenize(content)
    analysis_result = AnalysisResult(document_id=document.id, data=' '.join(words))
    db.session.add(analysis_result)

    # Сортировка документа (пример простейшей сортировки слов)
    sorted_words = sorted(words)
    sorting_result = SortingResult(document_id=document.id, sorted_data=' '.join(sorted_words))
    db.session.add(sorting_result)

    document.status = 'processed'
    db.session.commit()
