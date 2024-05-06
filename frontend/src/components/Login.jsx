import React, {useState} from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { toast } from 'react-toastify'

const Login = () => {
  const navigate = useNavigate()
  const [logindata, setLoginData] = useState({
    email: "",
    password: ""
  })
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e) => {
    setLoginData({...logindata, [e.target.name]: e.target.value})
  }
  
  const handleSubmit = async(e) => {
    e.preventDefault()
    const {email, password} = logindata
    if(!email || !password){
      setError("email and password are required")
    }
    else{
      setIsLoading(true)
      const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/login/", logindata)
      setIsLoading(false)
      const user = {
        'email': response.data.email,
        'names': response.data.full_name
      }
      console.log("response: ", response.data)
      if(response.status === 200){
        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('access', JSON.stringify(response.data.access_token))
        localStorage.setItem('refresh', JSON.stringify(response.data.refresh_token))
        navigate("/dashboard")
        // toast.success("login successful")
      }
    }
  }

  return (
    <div>
      <div className='form-container'>
        <div style={{width: "100%"}}  className='wrapper'>
          <h2>Login</h2>
          <form action="" onSubmit={handleSubmit}>
            {isLoading && (
              <p style={{color: "green"}}>Loading...</p>
            )}
            <div className='form-group'>
              <label htmlFor=""> Email Address:</label>
              <input type="text" 
                className='email-form' 
                name="email"
                value={logindata.email}
                onChange={handleChange}
              />
            </div>
            <div className='form-group'>
              <label htmlFor=""> Password:</label>
              <input type="password" 
              className='email-form' 
              name="password" 
              value={logindata.password}
              onChange={handleChange}
            />
            </div>
            <input type="submit" value="Login" className='submitButton' />
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login