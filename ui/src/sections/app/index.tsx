import './styles.css'
import { Layout, Pagination } from 'antd'
import { Content, Footer } from 'antd/es/layout/layout'
import { Search } from '../search'
import { Gallery } from '../gallery'
import { AppHeader } from '../header'
import { useState } from 'react'
import { UsersData } from '../../lib/types'
import { Paginator } from '../paginator'

function App() {

  const [ userData, setUserData ] = useState<UsersData | null>( null )

  const fetchUserData = async () => {
    const response = await fetch( "/api/users?page=1" );
    const userData: UsersData = await response.json();
    setUserData( userData )
  }

  const searchUsersByName = async ( name: string ) => {
    const response = await fetch( `/api/users/search/${ name }?page=1` );
    const userData: UsersData = await response.json();
    setUserData( userData )
  }

  return (
    <Layout>
      <AppHeader />
      <Content className="app-content">
        <Search fetchUserData={ fetchUserData } searchUsers={ searchUsersByName } />
        <Gallery fetchUserData={ fetchUserData } userData={ userData } />
        <Paginator userData={ userData } />
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
