### User Model

ref: https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#extending-the-existing-user-model

Based on my experience and information from the above sources, I think the best strategy
is to create a custom user model that extends the Django ``AbstractBaseUser`` model.
the difference between ```AbstractBaseUser``` and ```AbstractUser``` is that
```AbstractBaseUser``` provides more customization.

Also see: https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project
which clearly states changing to a custom user model mid-project is a bad idea. so it's always better to create
a custom user model at the beginning of the project as client requirements change unpredictably.


### Admin
my initial thought is strictly allowing only a single admin user can be problematic.
If the admin password is lost, then all admin functionality is lost.

but if it is the case, then I think we should add a custom management command to reset the admin password.
As a security point of view, only those who have access to the production server
could be able to reset the admin password.

of course, we can implement other type of password reset functionalities,
like sending an email to the admin user to reset the password. But I am assuming
that is beyond the scope of this project.



### Environment Variables
I think the best way to set up the environment variables is to use the ``.env`` file and
keep the secret key and other sensitive information in the ``.env`` file.


### User creation by admin
we need to define a custom permission to check if the user is an admin and use it to authenticate the admin user
in user creation view.

* the django user model provides a handy way to create a random password, I will use it.
* apparently we can't modify the `serializer.data` directly and the password serializer returns the hashed 
  password so need to override the `create` method of the view to return the plain text password.
