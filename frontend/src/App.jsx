import react from "react"
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import VerifyEmail from "./pages/VerifyEmail"
import UserSettings from "./pages/UserSettings"
import ViewProfile from "./pages/ViewProfile"
import PlayGame from "./pages/PlayGame"

function Logout(){
  localStorage.clear();
  return <Navigate to="/login"/>
}

// function RegisterAndLogout(){
//   localStorage.clear();
//   return <Register />
// }

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home/>
            </ProtectedRoute>
          }/>

          <Route path="/login" element={<Login/>}/>
          <Route path="/logout" element={<Logout/>}/>
          <Route path="/register" element={<Register/>}/>
          <Route path="/verify-email" element={<VerifyEmail/>}/>
          <Route path="/user/ID/:id" element={<ViewProfile/>}/>
          <Route path="/game/ID/:id" element={<PlayGame/>}/>

          <Route path="/settings" element={<ProtectedRoute><UserSettings/></ProtectedRoute>}/>
          <Route path="*" element={<NotFound/>}></Route>
          
        </Routes>
      </BrowserRouter>
  )
}

export default App
