import { Routes, Route } from "react-router-dom"
import Login from "./pages/(auth)/login/page"
import SignUp from "./pages/(auth)/signUp/page"
import Dashboard from "./pages/(protected)/dashboard/page"
function App() {
  return (
    <Routes>
      <Route path='/' element={<Login />} />
      <Route path='/sign-up' element={<SignUp />} />
      <Route path='/dashboard' element={<Dashboard />} />
    </Routes>
  )
}

export default App
