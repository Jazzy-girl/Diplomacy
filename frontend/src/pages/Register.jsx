import Form from "../components/Form"

function Register(){
    //return <Form route="/api/user/register/" method="register"/>
    return <Form route="/dj-rest-auth/registration/" method="register"/>
}

export default Register