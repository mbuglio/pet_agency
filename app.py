from flask import Flask, render_template, redirect, request, flash, url_for
from models import connect_db, db, Pet  
from forms import AddPetForm, EditPetForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:K1ashmir!@localhost:5432/pet_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'shh1234'

connect_db(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()


@app.route('/')
def home_page():
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():
    form = AddPetForm()
    
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_pet_form.html', form=form)

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_pet_form(id):
    
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        return redirect(url_for('show_pet_info', id=id))
    
    else:
        return render_template('edit_pet_form.html', form=form)

@app.route('/<int:id>', methods=['GET'])
def show_pet_info(id):
    pet = Pet.query.get_or_404(id)

    print("DEBUG: pet =", pet)  # Check the console or terminal for this output
    return render_template('pet_info.html', pet=pet)

@app.route('/adopted',methods=['GET'])
def show_adopted_pets():
    pets = Pet.query.filter_by(available = False).all()
    print("DEBUG: pets =", pets)
    
    return render_template('adopted_pet.html', pets=pets)


        



