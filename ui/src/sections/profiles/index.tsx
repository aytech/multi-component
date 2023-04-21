import { Button, Empty, List, Skeleton } from "antd"
import { Gallery } from "../gallery"
import { Paginator } from "../paginator"
import { Search } from "../search"
import { useEffect, useState } from "react"
import { Page, UsersData } from "../../lib/types"
import { UrlUtility } from "../../lib/utilities"
import { useSearchParams } from "react-router-dom"

interface Props {
  errorMessage: ( message: string ) => void
  successMessage: ( message: string ) => void
}

export const Profiles = ( {
  errorMessage,
  successMessage
}: Props ) => {

  const [ searchParams ] = useSearchParams()

  const [ userData, setUserData ] = useState<UsersData | null>( null )
  const [ loading, setLoading ] = useState<boolean>( true )
  const [ currentPage, setCurrentPage ] = useState<Page>( { page: 1, size: 10 } )

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

  useEffect( () => {
    fetchUserData()
  }, [ searchParams ] )

  const PageContent = () => userData !== undefined && userData !== null && userData.total > 0 ? (
    <>
      <Search searchParams={ searchParams } />
      <Gallery
        errorMessage={ errorMessage }
        refetch={ fetchUserData }
        searchParams={ searchParams }
        successMessage={ successMessage }
        userData={ userData } />
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

  return (
    <AppContent />
  )
}