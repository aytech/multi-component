import './styles.css'
import { Layout } from 'antd'
import { Content, Footer } from 'antd/es/layout/layout'
import { Search } from '../search'
import { Gallery } from '../gallery'
import { AppHeader } from '../header'
import { useEffect, useState } from 'react'
import { Page, UsersData } from '../../lib/types'
import { Paginator } from '../paginator'
import { Route, Routes, useSearchParams } from 'react-router-dom'

function App() {

  const [ searchParams ] = useSearchParams();
  const [ currentPage, setCurrentPage ] = useState<Page>( { page: 1, size: 10 } )

  const [ userData, setUserData ] = useState<UsersData | null>( null )

  const getSearchParameters = (): Page => {
    const parameters = { page: currentPage.page, size: currentPage.size }
    let page: number | string | null = searchParams.get( "page" )
    let size: number | string | null = searchParams.get( "size" )
    if ( page !== null ) {
      page = parseInt( page )
      parameters.page = Number.isNaN( page ) ? 1 : page
    }
    if ( size !== null ) {
      size = parseInt( size )
      parameters.size = Number.isNaN( size ) ? 10 : size
    }
    return parameters
  }

  const fetchUserData = async () => {
    const parameters: Page = getSearchParameters()
    setCurrentPage( parameters )
    const response = await fetch( `/api/users?page=${ parameters.page }&size=${ parameters.size }` );
    const userData: UsersData = await response.json();
    setUserData( userData )
  }

  const searchUsersByName = async ( name: string ) => {
    const response = await fetch( `/api/users/search/${ name }?page=${ currentPage.page }&size=${ currentPage.size }` );
    const userData: UsersData = await response.json();
    setUserData( userData )
  }

  const AppContent = () => (
    <>
      <Search fetchUserData={ fetchUserData } searchUsers={ searchUsersByName } />
      <Gallery userData={ userData } />
      <Paginator currentPage={ currentPage } loadPage={ fetchUserData } userData={ userData } />
    </>
  )

  useEffect( () => {
    fetchUserData()
  }, [ searchParams ] )

  return (
    <Layout>
      <AppHeader />
      <Content className="app-content">
        <Routes>
          <Route path="/" element={ <AppContent /> } />
        </Routes>
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
