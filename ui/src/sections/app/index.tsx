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
import { UrlUtility } from '../../lib/utilities'

export const App = () => {

  const [ searchParams ] = useSearchParams()

  const [ currentPage, setCurrentPage ] = useState<Page>( { page: 1, size: 10 } )
  const [ userData, setUserData ] = useState<UsersData | null>( null )
  const [ loading, setLoading ] = useState<boolean>( true )

  const fetchUserData = async () => {
    setLoading( true )
    const parameters: Page = UrlUtility.getSearchParameters( searchParams, currentPage.page, currentPage.size )
    setCurrentPage( parameters )
    const requestUrl = parameters.search !== undefined
      ? UrlUtility.getUserSearchUrl( parameters )
      : UrlUtility.getUsersUrl( parameters )
    const response = await fetch( requestUrl );
    const userData: UsersData = await response.json();
    setUserData( userData )
    setLoading( false )
  }

  const PageContent = () => userData !== undefined && userData !== null && userData.total > 0 ? (
    <>
      <Search searchParams={ searchParams } />
      <Gallery refetch={ fetchUserData } searchParams={ searchParams } userData={ userData } />
      <Paginator currentPage={ currentPage } searchParams={ searchParams } userData={ userData } />
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
