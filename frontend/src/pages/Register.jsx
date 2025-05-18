import RegisterForm from "../components/RegisterForm"

function Register(){
    return <RegisterForm route="/dj-rest-auth/registration/" method="register"/>
}

export default Register