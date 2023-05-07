import { Input } from "antd"
import "./styles.css"
import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"

interface Props {
  paginationEnabled: boolean
  searchParams: URLSearchParams
}

export const Search = ( {
  paginationEnabled,
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
    if ( paginationEnabled === true ) {
      searchParams.set( "page", "1" )
    }
    return navigate( `${ location.pathname }?${ searchParams.toString() }` )
  };

  return (
    <Search
      allowClear
      className="search-bar"
      enterButton
      onChange={ ( event: any ) => {
        if ( event.target.value === "" ) { // clear action
          setSearchValue( "" )
          searchParams.delete( "search" )
          return navigate( `${ location.pathname }?${ searchParams.toString() }` )
        } else {
          setSearchValue( event.target.value )
        }
      } }
      onSearch={ onSearch }
      placeholder="input search text"
      value={ searchValue } />
  )
}