import React, {useState} from 'react'
import axios from 'axios'
import {useNavigate} from 'react-router-dom'
import { toast } from 'react-toastify'

const Signup = () => {
  const navigate = useNavigate()
  const [formdata, setFormdata] = useState({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    password2: ""
  })

  const [error, setError] = useState("")

  const {email, first_name, last_name, password, password2} = formdata
  const handleChange = (e) => {
    setFormdata({...formdata, [e.target.name]: e.target.value})
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if(!email || !first_name || !last_name || !password || !password2){
      setError('Please fill in all fields')
    }
    else{
      console.log("formdata: ", formdata)
      const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/register/", formdata)
      console.log("response: ",response.data)
      if(response.status === 201){
        navigate("/otp/verify")
        // toast.success(response.data.message)
      }
    }
  }

  return (
    <div>
      <div className='form-container'>
        <div style={{width: "100%"}}  className='wrapper'>
          <h2>Create Account</h2>
          <p style={{color: "red", padding: "1px"}}>{error ? error : ""} </p>
          <form action="" onSubmit={handleSubmit}>
            <div className='form-group'>
              <label htmlFor=""> Email Address:</label>
              <input type="text" 
                className='email-form' 
                name="email" 
                value={email}
                onChange = {handleChange}
              />
            </div>
            <div className='form-group'>
              <label htmlFor=""> First Name:</label>
              <input type="text" 
                className='email-form' 
                name="first_name" 
                value={first_name} 
                onChange = {handleChange}
              />
            </div>
            <div className='form-group'>
              <label htmlFor=""> Last Name:</label>
              <input type="text" 
                className='email-form' 
                name="last_name" 
                value={last_name} 
                onChange = {handleChange}
              />
            </div>
            <div className='form-group'>
              <label htmlFor=""> Password:</label>
              <input type="password" 
                className='email-form' 
                name="password" 
                value={password} 
                onChange = {handleChange}
              />
            </div>
            <div className='form-group'>
              <label htmlFor=""> Confirm Password:</label>
              <input type="password" 
                className='email-form' 
                name="password2" 
                value={password2} 
                onChange = {handleChange}
              />
            </div>
            <input type="submit" value="submit" className='submitButton' />
          </form>
          <h3 className='text-option'>Or</h3>
          <div className='githubContainer'>
            <button>Sign up with GitHub</button>
          </div>
          <div className='googleContainer'>
            <button>Sign up with Google</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Signup