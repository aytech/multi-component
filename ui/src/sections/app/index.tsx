import './styles.css'
import { Layout } from 'antd'
import { Content, Footer } from 'antd/es/layout/layout'
import { Search } from '../search'
import { Gallery } from '../gallery'
import { AppHeader } from '../header'
import { useState } from 'react'
import { Profile } from '../../lib/types'

function App() {

  const [ profiles, setProfiles ] = useState<Array<Profile>>( [] )

  const fetchProfiles = async () => {
    const response = await fetch( "/api/users?page=1" );
    const profiles: Array<Profile> = await response.json();
    setProfiles( profiles )
  }

  const searchProfilesByName = async ( name: string ) => {
    const response = await fetch( `/api/users/search/${ name }?page=1` );
    const profiles: Array<Profile> = await response.json();
    setProfiles( profiles )
  }

  return (
    <Layout>
      <AppHeader />
      <Content className="app-content">
        <Search fetchProfiles={ fetchProfiles } searchProfiles={ searchProfilesByName } />
        <Gallery fetchProfiles={ fetchProfiles } profiles={ profiles } />
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
