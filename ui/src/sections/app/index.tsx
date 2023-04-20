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
    const parameters: Page = { page: currentPage.page, size: currentPage.size }
    let page: number | string | null = searchParams.get( "page" )
    let size: number | string | null = searchParams.get( "size" )
    let search: string | null = searchParams.get( "search" )
    if ( page !== null ) {
      page = parseInt( page )
      parameters.page = Number.isNaN( page ) ? 1 : page
    }
    if ( size !== null ) {
      size = parseInt( size )
      parameters.size = Number.isNaN( size ) ? 10 : size
    }
    if ( search !== null && search.trim() !== "" ) {
      parameters.search = search
    }
    return parameters
  }

  const fetchUserData = async () => {
    setLoading( true )
    const parameters: Page = getSearchParameters()
    setCurrentPage( parameters )
    const requestUrl = parameters.search !== undefined
      ? `/api/users/search/${ parameters.search }?page=${ currentPage.page }&size=${ currentPage.size }`
      : `/api/users?page=${ parameters.page }&size=${ parameters.size }`
    const response = await fetch( requestUrl );
    const userData: UsersData = await response.json();
    setUserData( userData )
    setLoading( false )
  }

  const PageContent = () => userData !== undefined && userData !== null && userData.total > 0 ? (
    <>
      <Search searchParams={ searchParams } />
      <Gallery refetch={ fetchUserData } userData={ userData } />
      <Paginator currentPage={ currentPage } loadPage={ fetchUserData } userData={ userData } />
    </>
  ) : (
    <>
      <Search searchParams={ searchParams } />
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
