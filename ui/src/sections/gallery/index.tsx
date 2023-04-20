import { Row } from "antd"
import "./styles.css"
import { UsersData } from "../../lib/types"
import { GalleryItem } from "./components/item"

interface Props {
  errorMessage: ( message: string ) => void
  refetch: () => void
  searchParams: URLSearchParams
  successMessage: ( message: string ) => void
  userData: UsersData | null
}

export const Gallery = ( {
  errorMessage,
  refetch,
  searchParams,
  successMessage,
  userData
}: Props ) => {

  const GalleryCollection = () => userData !== null ? (
    <>
      { userData.users.map( profile => (
        <GalleryItem
          errorMessage={ errorMessage }
          profile={ profile }
          refetch={ refetch }
          searchParams={ searchParams }
          successMessage={ successMessage } />
      ) ) }
    </>
  ) : null

  return (
    <Row gutter={ 16 }>
      <GalleryCollection />
    </Row>
  )
}