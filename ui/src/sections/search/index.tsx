import { Col, Row, Input } from "antd"
import "./styles.css"

interface Props {
  fetchUserData: () => void
  searchUsers: ( name: string ) => void
}

export const Search = ( {
  fetchUserData,
  searchUsers
}: Props ) => {

  const { Search } = Input

  const onSearch = async ( value: string ) => {
    if ( value.length > 0 ) {
      searchUsers( value )
    } else {
      fetchUserData()
    }
  };

  return (
    <Row className="search-bar">
      <Col xs={ 24 } sm={ 22 } md={ 20 } lg={ 20 } xl={ 20 }>
        <Search allowClear placeholder="input search text" onSearch={ onSearch } enterButton />
      </Col>
    </Row>
  )
}