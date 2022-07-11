# INTERNFAIR

Helps match Interns to openings and Employers to Interns
This Project is built with
- Python, Flask, SQLAlchemy, Postgresql, JWT
Project uses MVC

## Dependecies

The program has no dependency save python >= 3.6


## API Documentation

EndPoints
UserController Endpoints
- @route /register
- @method POST
- @access PUBLIC
- @headers {...}
-@user {
        email: string,
        password: string,
        confirm_password: string
    }
- @desc 
    registers user to the application
- @ returns {
    201} 0r 404 if error

## Example Usage

/register

## License

Mars Software




