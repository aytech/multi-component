import './styles.css'
import { Button, Empty, Layout, List, Skeleton } from 'antd'
import { Content, Footer } from 'antd/es/layout/layout'
import { Search } from '../search'
import { Gallery } from '../gallery'
import { AppHeader } from '../header'
import { useEffect, useState } from 'react'
import { Page, UsersData } from '../../lib/types'
import { Paginator } from '../paginator'
import { useSearchParams } from 'react-router-dom'

function App() {

  const [ searchParams ] = useSearchParams()

  const [ currentPage, setCurrentPage ] = useState<Page>( { page: 1, size: 10 } )
  const [ userData, setUserData ] = useState<UsersData | null>( null )
  const [ loading, setLoading ] = useState<boolean>( true )

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
    setLoading( true )
    const parameters: Page = getSearchParameters()
    setCurrentPage( parameters )
    const response = await fetch( `/api/users?page=${ parameters.page }&size=${ parameters.size }` );
    const userData: UsersData = await response.json();
    setUserData( userData )
    setLoading( false )
  }

  const searchUsersByName = async ( name: string ) => {
    const response = await fetch( `/api/users/search/${ name }?page=${ currentPage.page }&size=${ currentPage.size }` );
    const userData: UsersData = await response.json();
    setUserData( userData )
  }

  const PageContent = () => userData !== undefined && userData !== null && userData.total > 0 ? (
    <>
      <Search fetchUserData={ fetchUserData } searchUsers={ searchUsersByName } />
      <Gallery userData={ userData } />
      <Paginator currentPage={ currentPage } loadPage={ fetchUserData } userData={ userData } />
    </>
  ) : (
    <>
      <Search fetchUserData={ fetchUserData } searchUsers={ searchUsersByName } />
      <Empty description="No profiles found">
        <Button
          type="primary"
          onClick={ fetchUserData }>
          Go back
        </Button>
      </Empty>
    </>
  )

  const AppContent = () => loading ? (
    <>
      { [ 1, 2, 3, 4, 5 ].map( ( key ) => (
        <Skeleton loading active avatar key={ key }>
          <List.Item.Meta avatar={ <Skeleton.Image /> } />
        </Skeleton>
      ) ) }
    </>
  ) : (
    <PageContent />
  )

  useEffect( () => {
    fetchUserData()
  }, [ searchParams ] )

  return (
    <Layout>
      <AppHeader />
      <Content className="app-content">
        <AppContent />
      </Content>
      <Footer>Footer</Footer>
    </Layout>
  )
}

export default App
