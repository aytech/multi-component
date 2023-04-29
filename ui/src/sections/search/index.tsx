import { Col, Row, Input } from "antd"
import "./styles.css"
import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"

interface Props {
  searchParams: URLSearchParams
}

export const Search = ( {
  searchParams
}: Props ) => {

  const location = useLocation()
  const navigate = useNavigate()

  const { Search } = Input

  const [ searchValue, setSearchValue ] = useState<string>( searchParams.get( "search" ) || "" )

  const onSearch = async () => {
    if ( searchValue === "" ) {
      searchParams.delete( "search" )
    } else {
      searchParams.set( "search", searchValue )
    }
    searchParams.set( "page", "1" )
    return navigate( `${ location.pathname }?${ searchParams.toString() }` )
  };

  return (
    <Row className="search-bar">
      <Col xs={ 24 } sm={ 22 } md={ 20 } lg={ 20 } xl={ 20 }>
        <Search
          allowClear
          enterButton
          onChange={ ( event: any ) => setSearchValue( event.target.value ) }
          onSearch={ onSearch }
          placeholder="input search text"
          value={ searchValue } />
      </Col>
    </Row>
  )
}