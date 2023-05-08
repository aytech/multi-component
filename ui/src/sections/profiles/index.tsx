import { Button, Col, Empty, List, Radio, Row, Skeleton } from "antd"
import { Gallery } from "../gallery"
import { Paginator } from "../paginator"
import { Search } from "../search"
import { useEffect, useState } from "react"
import { Page, UsersData } from "../../lib/types"
import { UrlUtility } from "../../lib/utilities"
import { useLocation, useNavigate, useSearchParams } from "react-router-dom"
import "./styles.css"

interface Props {
  errorMessage: ( message: string ) => void
  successMessage: ( message: string ) => void
}

export const Profiles = ( {
  errorMessage,
  successMessage
}: Props ) => {

  const location = useLocation()
  const navigate = useNavigate()

  const [ searchParams ] = useSearchParams()


  const [ currentPage, setCurrentPage ] = useState<Page>( { page: 1, size: 10 } )
  const [ loading, setLoading ] = useState<boolean>( true )
  const [ statusValue, setStatusValue ] = useState<string>()
  const [ userData, setUserData ] = useState<UsersData | null>( null )

  const fetchUserData = async () => {
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

  const filterStatuses = ( event: any ) => {
    const status: string = event.target.value
    if ( status === "liked" || status === "scheduled" || status === "new" ) {
      setStatusValue( status )
      searchParams.set( "status", status )
      navigate( `${ location.pathname }?${ searchParams.toString() }` )
    }
  }

  useEffect( () => {
    fetchUserData()
    setStatusValue( searchParams.get( "status" ) || undefined )
  }, [ searchParams ] )

  const PageContent = () => userData !== undefined && userData !== null && userData.total > 0 ? (
    <>
      <Row>
        <Col xs={ 24 } sm={ 24 } md={ 12 } lg={ 14 } xl={ 16 }>
          <Search paginationEnabled={ true } searchParams={ searchParams } />
        </Col>
        <Col xs={ 24 } sm={ 24 } md={ 11 } lg={ 9 } xl={ 7 } offset={ 1 }>
          <Radio.Group className="status-selector" onChange={ filterStatuses } value={ statusValue }>
            <Radio value="liked">Liked</Radio>
            <Radio value="scheduled">Scheduled</Radio>
            <Radio value="new">New</Radio>
          </Radio.Group>
        </Col>
      </Row>

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
      <Search paginationEnabled={ true } searchParams={ searchParams } />
      <Empty description="No profiles found">
        <Button
          type="primary"
          onClick={ () => {
            searchParams.delete( "search" )
            searchParams.delete( "status" )
            navigate( `${ location.pathname }?${ searchParams.toString() }` )
          } }>
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