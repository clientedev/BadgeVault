from app import app, db, init_db
from models import Student
from scraper import scrape_profile
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

# Initialize database tables
with app.app_context():
    init_db()


@app.route('/')
def index():
    students = Student.query.order_by(Student.created_at.desc()).all()
    
    total_badges = sum(s.badge_count for s in students)
    total_students = len(students)
    avg_badges = round(total_badges / total_students, 1) if total_students > 0 else 0
    max_badges = max((s.badge_count for s in students), default=0)
    
    metrics = {
        'total_badges': total_badges,
        'total_students': total_students,
        'avg_badges': avg_badges,
        'max_badges': max_badges
    }
    
    students_data = [s.to_dict() for s in students]
    
    return render_template('index.html', students=students, students_data=students_data, metrics=metrics)


@app.route('/add_student', methods=['POST'])
def add_student():
    profile_url = request.form.get('profile_url', '').strip()
    
    if not profile_url:
        flash('Por favor, insira um link válido.', 'error')
        return redirect(url_for('index'))
    
    try:
        app.logger.info(f'Tentando adicionar perfil: {profile_url}')
        data = scrape_profile(profile_url)
        app.logger.info(f'Dados extraídos: {data}')
        
        student = Student(
            name=data['name'],
            badge_count=data['badge_count'],
            profile_url=profile_url,
            platform=data['platform']
        )
        
        db.session.add(student)
        db.session.commit()
        
        flash(f'Aluno {data["name"]} adicionado com sucesso! {data["badge_count"]} badges encontradas.', 'success')
    except IntegrityError:
        db.session.rollback()
        app.logger.error('Perfil duplicado tentou ser adicionado')
        flash('Este perfil já foi adicionado.', 'error')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Erro ao adicionar aluno: {str(e)}', exc_info=True)
        flash(str(e), 'error')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
