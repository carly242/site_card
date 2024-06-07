from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  ListView, UpdateView, DeleteView, CreateView
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse, reverse_lazy
from .forms import DocumentForm, UserForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.conf import settings


from .models import User, Document
import base64
from django.contrib import messages

# Create your views here.
def test_media(request):
    image_url = settings.MEDIA_URL + 'User.png'
    return render(request, 'test_media.html', {'image_url': image_url})


from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import base64


def download_vcard(request, slug):
    # Obtenir les informations du profil
    user_profile = get_object_or_404(User, slug=slug)
    
    # Générez les données vCard
    vcard_data = 'BEGIN:VCARD\n'
    vcard_data += 'VERSION:3.0\n'
    vcard_data += 'FN:' + user_profile.name + '\n'  # Nom complet
    vcard_data += 'EMAIL:' + user_profile.email + '\n'  # Email
    vcard_data += 'EMAIL;TYPE=INTERNET:' + user_profile.email_bureau + '\n'  # Email bureau
    vcard_data += 'TEL;TYPE=CELL:' + user_profile.phone_number + '\n'  # Numéro de téléphone mobile
    vcard_data += 'TEL;TYPE=WORK:' + user_profile.office_number + '\n'  # Numéro de téléphone bureau

    try:
        if user_profile.photo and hasattr(user_profile.photo, 'file'):
            # Si l'utilisateur a une photo, lisez-la et encodez-la en base64
            photo_data = user_profile.photo.read()
            photo_base64 = base64.b64encode(photo_data).decode('utf-8')
            photo_content_type = 'image/jpeg'  # Remplacez par le type de contenu approprié
            vcard_data += 'PHOTO;ENCODING=BASE64;TYPE=' + photo_content_type + ':\n'
            vcard_data += photo_base64 + '\n'  # Photo
    except FileNotFoundError:
        pass  # Si le fichier photo n'est pas trouvé, continuez sans ajouter de photo à la vCard

    # Ajoutez le reste des champs et fermez la vCard
    vcard_data += 'END:VCARD'

    # Créez une réponse HTTP avec les données vCard
    response = HttpResponse(vcard_data, content_type='text/vcard')
    response['Content-Disposition'] = 'attachment; filename="contact.vcf"'
    return response






# Shared Views
def connxeion(request):
	return render(request, 'connexion/login.html')




from django.contrib import messages

def connect(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if 'first_login' not in request.session:
                # Stockez un indicateur dans la session de l'utilisateur pour marquer la première connexion
                request.session['first_login'] = True
                # Stockez également le slug de l'utilisateur dans la session pour référence future
                request.session['user_slug'] = user.slug
            if user.is_admin or user.is_superuser:
                return redirect('admin') 
            else:
                return redirect('profile', slug=user.slug)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        if request.user.is_authenticated:
            # Si l'utilisateur est déjà authentifié, redirigez-le vers son profil
            return redirect('profile', slug=request.user.slug)
    return render(request, 'connexion/login.html')



def deconnect(request):
    logout(request)
    if 'user_slug' in request.session:
        del request.session['user_slug']  # Supprimer le slug de la session
    messages.error(request, "Veillez vous conncter")
    return redirect('home')

def create(request):
    return render(request, 'connexion/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('created')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            return redirect('created')

        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Compte créé avec succès.')
        return redirect('home')
    else:
        return render(request, 'connexion/signup.html')



from django.urls import reverse


    
        

    # Renvoyez ces valeurs dans le contexte de votre template

def view_profile(request, slug=None):
    if slug is not None:
        user_profile = get_object_or_404(User, slug=slug)
    else:
        # Si aucun slug n'est fourni, vous pouvez fournir un comportement alternatif ici,
        # comme récupérer le profil de l'utilisateur actuellement connecté.
        # Par exemple, si vous stockez l'utilisateur connecté dans la session :
        user_profile = request.session.get('current_user_profile', None)
        if user_profile is None:
            # Gérer le cas où aucun utilisateur n'est connecté ou s'il n'y a pas de profil enregistré dans la session
            return redirect(reverse('home'))  # Rediriger vers la page de connexion par exemple

    return render(request, 'dashboard/index.html', {'user_profile': user_profile})










@login_required
def client(request):
	return render(request, 'dashboard/finances.html')






from django.shortcuts import get_object_or_404, render
from .models import User

@login_required
def edit_profile(request):
    user_profile = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        return redirect('profile', slug=user_profile.slug)
    else:
        # Utilisez la méthode initial du formulaire pour définir les valeurs par défaut
        initial_data = {
            'name': user_profile.name if user_profile.name else 'Your Name',
            'function': user_profile.function if user_profile.function else 'Function',
            'email': user_profile.email if user_profile.email else 'Email',
            'email_bureau': user_profile.email_bureau if user_profile.email_bureau else 'Office Email',
            'city': user_profile.city if user_profile.city else 'adress',
            'adress_link': user_profile.adress_link if user_profile.adress_link else '#',
            'phone_number': user_profile.phone_number if user_profile.phone_number else 'Phone Number',
            'office_number': user_profile.office_number if user_profile.office_number else 'Office Number',
            'website': user_profile.website if user_profile.website else 'Website',
            # Ajoutez d'autres champs ici avec leurs valeurs par défaut
        }
        form = UserForm(instance=user_profile, initial=initial_data)
    return render(request, 'dashboard/edit_profil.html', {'form': form})






def login_or_edit_profile(request):
    if request.user.is_authenticated:
        if 'first_login' in request.session:
            # Si l'utilisateur s'est déjà connecté avec succès mais n'est pas un nouvel utilisateur,
            # redirigez-le vers la page où il doit saisir son mot de passe pour accéder aux fonctionnalités supplémentaires.
            return redirect(reverse('testify'))
        else:
            # Si c'est la première connexion réussie, redirigez-le directement vers la page de modification de profil.
            return redirect(reverse('edit_profile'))
    else:
        # Si l'utilisateur n'est pas connecté du tout, redirigez-le vers la page de connexion.
        return redirect('home')


def login_or_functions(request):
    if request.user.is_authenticated:
        if 'first_login' in request.session:
            # Si l'utilisateur s'est déjà connecté avec succès mais n'est pas un nouvel utilisateur,
            # redirigez-le vers la page où il doit saisir son mot de passe pour accéder aux fonctionnalités supplémentaires.
            return redirect(reverse('testify'))
        else:
            # Si c'est la première connexion réussie, redirigez-le directement vers la page de modification de profil.
            return redirect(reverse('fonctionalite'))
    else:
        # Si l'utilisateur n'est pas connecté du tout, redirigez-le vers la page de connexion.
        return redirect('home')

@login_required
def check_password_for_fonctionnalite(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user  # Utilisateur actuellement connecté
        if user.check_password(entered_password):
            return redirect('edit_profile')  # Redirige vers les fonctionnalités supplémentaires si le mot de passe est correct
        else:
            # Afficher un message d'erreur si le mot de passe est incorrect
            return render(request, 'dashboard/incorrect_pass.html')
    elif request.method == 'GET':
        return render(request, 'dashboard/check_password.html')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])
    



@login_required
def check_password_for_menu(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user  # Utilisateur actuellement connecté
        if user.check_password(entered_password):
            return redirect('menu')  # Redirige vers les fonctionnalités supplémentaires si le mot de passe est correct
        else:
            # Afficher un message d'erreur si le mot de passe est incorrect
            return render(request, 'dashboard/incorrect_pass.html')
    elif request.method == 'GET':
        return render(request, 'dashboard/check_password.html')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])





def check_pass(request):
    return render(request,'dashboard/checkpass.html' )
"""

def password_change_form(request):
    return render(request, 'dashboard/change_password.html')

from django.contrib import messages

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Pour maintenir l'utilisateur connecté
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('pass_changer')  # Rediriger vers une page de succès par exemple
        else:
            # Si la validation du formulaire échoue, cela peut être dû à un ancien mot de passe incorrect
            # Ajouter un message d'erreur pour informer l'utilisateur
            messages.error(request, 'Le mot de passe actuel est incorrect. Veuillez réessayer.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {'form': form})



def password_change_done(request):
    return render(request, 'dashboard/change_password_done.html')
"""

def change_password(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Vérifie si l'utilisateur est authentifié
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('pass_changer')
        else:
            return redirect('connect')  # Redirigez l'utilisateur non authentifié vers la page de connexion
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {'form': form})



def password_success(request):
    return render(request, 'dashboard/change_password_done.html')

User = get_user_model()
from django.contrib import messages

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Vérifie si l'utilisateur est authentifié
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                # Mettre à jour le hachage d'authentification de la session utilisateur
                update_session_auth_hash(request, request.user)
                # Ajouter un message de succès
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès. Veuillez vous connecter avec le nouveau mot de passe.")
                # Redirection vers la page de connexion
                return redirect('pass_effectue')
        else:
            # Redirection de l'utilisateur non authentifié vers la page de connexion
            
            return redirect('connect')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'dashboard/password_reset_confirm.html', {'form': form})



"""
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'dashboard/password_reset_confirm.html'
    form_class = CustomSetPasswordForm  # Utiliser la sous-classe personnalisée
    success_url = reverse_lazy('password_reset_complete')
"""  

@login_required
def aabook_form(request):
	return render(request, 'dashboard/add_pdf.html')



@login_required
def aabook(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            pdf = form.cleaned_data['pdf']
            current_user = request.user

            # Création d'un document lié à l'utilisateur actuel
            document = Document(title=title, pdf=pdf, user=current_user)
            document.save()
            
            messages.success(request, 'Ajout réussi')
            return redirect('albook')  # Rediriger vers la liste des documents après ajout
        else:
            messages.error(request, 'Erreur lors de l\'ajout du document')
            return render(request, 'dashboard/add_pdf.html', {'form': form})  # Afficher à nouveau le formulaire avec les erreurs
    else:
        form = DocumentForm()
        return render(request, 'dashboard/add_pdf.html', {'form': form})  # Afficher le formulaire pour la première fois
 
 

class ABookListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'dashboard/list_pdf.html'
    context_object_name = 'docs'
    paginate_by = 3

    def get_queryset(self):
        # Filtrer les documents en fonction de l'utilisateur connecté
        return Document.objects.filter(user_id=self.request.user.id).order_by('-id')
    
"""   
class AManageUserprofil(LoginRequiredMixin, ListView):
    model= UserProfile
    template_name = 'dashboard/manage_profil.html'
    context_object_name = 'Uses'
    paginate_by= 3
    
    def get_queryset(self) -> QuerySet[Any]:
         return UserProfile.objects.order_by('name')
""" 


def PageBuilding(request):
    return render(request, 'dashboard/page_not_done.html')


class AeditView(LoginRequiredMixin, UpdateView):
    model= User
    form_class = UserForm
    template_name= 'dashboard/edit_profil.html'
    success_url= reverse_lazy('home')
    success_message = 'Sauvegarder avec succés'
    

@login_required
def Menu(request):
	return render(request, 'dashboard/menu.html')


def login_or_menu(request):
    if request.user.is_authenticated:
        return redirect(reverse('menu'))
    else:
        return redirect('connect')

@login_required
def Transport(request):
	return render(request, 'dashboard/transport.html')


@login_required
def Finance(request):
	return render(request, 'dashboard/finances.html')



class AManageBook(LoginRequiredMixin,ListView):
	model = Document
	template_name = 'dashboard/manage.html'
	context_object_name = 'docs'
	paginate_by = 3

	def get_queryset(self):
            return Document.objects.filter(user=self.request.user).order_by('-id')


class AeditDocView(LoginRequiredMixin, UpdateView):
    model= Document
    form_class = DocumentForm
    template_name= 'dashboard/edit_doc.html'
    success_url= reverse_lazy('ambook')
    success_message = 'Sauvegarder avec succés'
    


class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Document
	template_name = 'dashboard/delete.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was dele successfully'
 
 
 
 
 #admin
def dashboard(request):
	user = User.objects.all().count()

	context = { 'user':user}

	return render(request, 'admin/home.html', context)
    
def create_user_form(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}

    return render(request, 'admin/add_user.html', choice)


class ListUserView(generic.ListView):
    model = User
    template_name = 'admin/list_user.html'
    context_object_name = 'users'
    paginate_by = 4
 
class CreateUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'admin/add_user.html'
    success_message = 'Compte utilisateur créé avec succès'

    def get_success_url(self):
    # Récupérer l'utilisateur créé
     created_user = self.object
    # Rediriger vers la page de profil de l'utilisateur créé en utilisant son nom
     return reverse_lazy('profile_detail', kwargs={'name': created_user.name})

""" 
def create_user_form(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}

    return render(request, 'admin/add_user.html', choice)

from django.contrib.auth.models import User

from .models import User  # Importez votre modèle User

def create_user(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        email_bureau = request.POST['email_bureau']
        number = request.POST['numero']
        office_number = request.POST['numero_bureau']
        adress = request.POST['city']
        site = request.POST['website']
        photo = request.FILES['image']
        password = request.POST['password']
        password = make_password(password)
        userType=request.POST['userType']
        
        # Utilisez le gestionnaire personnalisé CustomUserManager pour créer un utilisateur
        #user_manager = User.objects
        if userType == "client":
            user = User.objects.create_user(name=name,  email=email, email_bureau= email_bureau, phone_number =number, office_number= office_number, photo=photo, password=password, city= adress, website= site,is_client=True)

            messages.success(request, 'Member was created successfully!')
            return redirect('wluser')
        elif userType == "Admin":
            user = User.objects.create_user(name=name, email=email, email_bureau= email_bureau, phone_number =number, office_number= office_number, photo= photo, password=password,city= adress, website= site,is_admin=True)
            
            messages.success(request, 'Member was created successfully!')
            return redirect('wluser')   
        else:
            messages.success(request, 'Member was not created')
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')
"""  



class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = UserForm
    template_name = 'admin/edit_user.html'
    success_url = reverse_lazy('wluser')
    success_message = "Data successfully updated"
    

class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='admin/delete_user.html'
    success_url = reverse_lazy('wluser')
    success_message = "Data successfully deleted"