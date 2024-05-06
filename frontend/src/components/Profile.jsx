import React, {useEffect} from 'react'
import {useNavigate} from 'react-router-dom'
import AxiosInstance from '../utils/AxiosInstance'

const Profile = () => {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user'))
  const jwt_access = JSON.parse(localStorage.getItem('access'))

  const getSomeData = async () => {
    const res = await AxiosInstance.get('/auth/profile/')
    console.log(res)
  }

  useEffect(() => {
    if(jwt_access === null && !user){
      navigate('/login')
    }
    else{
      console.log("=======Get Some Data=======")
      getSomeData()
    }
  }, [jwt_access, user])
  const refresh = JSON.parse(localStorage.getItem('refresh'))

  const handleLogout = async () => {
    const res = await AxiosInstance.post('/auth/logout/', {"refresh_token": refresh})
    if(res.status === 200){
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
      navigate('/login')
    }
  }

  return (
    <div className='container'>
      <h2>hi {user && user.names}</h2>
      <p style={{textAlign:'center',}}>welcome to your profile</p>
      <button onClick={handleLogout} className='logout-btn'>Logout</button>
    </div>
  )
}

export default Profile