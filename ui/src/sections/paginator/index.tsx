import { Pagination } from "antd"
import { Page, UsersData } from "../../lib/types"
import { useLocation, useNavigate } from "react-router-dom"
import "./styles.css"

interface Props {
  currentPage: Page
  searchParams: URLSearchParams
  userData: UsersData | null
}

export const Paginator = ( {
  currentPage,
  searchParams,
  userData
}: Props ) => {

  const location = useLocation()
  const navigate = useNavigate()

  const onPageChange = ( page: number ) => {
    if ( page !== currentPage.page ) {
      searchParams.set( "page", page.toString() )
      return navigate( `${ location.pathname }?${ searchParams.toString() }` )
    }
  }

  const onPageSizeChange = ( _: number, size: number ) => {
    searchParams.set( "size", size.toString() )
    return navigate( `${ location.pathname }?${ searchParams.toString() }` )
  }

  return userData !== null ? (
    <Pagination
      className="pagination"
      defaultCurrent={ currentPage.page }
      onChange={ onPageChange }
      onShowSizeChange={ onPageSizeChange }
      defaultPageSize={ currentPage.size }
      showSizeChanger
      total={ userData.total }
    />
  ) : null
}