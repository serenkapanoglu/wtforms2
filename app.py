from flask import Flask,request, render_template, flash, redirect

from models import db, connet_db, Pet

from forms import AddPetForm
from forms import PetForm

app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

db.init_app(app)



@app.route('/')
def root():
    pets = Pet.query.all()
    return render_template("show.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    
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
        
        return redirect(f"/pets/{pet.id}")
    
    return render_template("pet_add_form.html", form=form)
        
@app.route('/pets/<int:uid>', methods=["GET", "POST"])
def pet_details(uid):
    pet = Pet.query.get_or_404(uid)
    form = PetForm(obj=pet)
    
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        flash(f"Pet {uid} updated!")
        return redirect(f"/pets/{uid}")
    
    return render_template("pet_form.html", pet=pet, form=form)
