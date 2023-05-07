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

  const isScheduled = ( profile_id: number ) => {
    return userData?.scheduled !== undefined && userData.scheduled.indexOf( profile_id ) !== -1
  }

  const GalleryCollection = () => userData !== null ? (
    <>
      { userData.users.map( profile => (
        <GalleryItem
          errorMessage={ errorMessage }
          key={ profile.id }
          profile={ profile }
          refetch={ refetch }
          scheduled={ isScheduled( profile.id ) }
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