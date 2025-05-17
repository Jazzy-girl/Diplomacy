import RegisterForm from "../components/RegisterForm"

function Login(){
    return <RegisterForm route="/api/token/" method="login"/>
}

export default Login