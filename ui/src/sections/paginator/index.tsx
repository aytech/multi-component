import { Pagination } from "antd"
import { Page, UsersData } from "../../lib/types"
import { useNavigate } from "react-router-dom"
import "./styles.css"

interface Props {
  currentPage: Page
  loadPage: ( page: number, pageSize: number ) => void
  userData: UsersData | null
}

export const Paginator = ( {
  currentPage,
  userData
}: Props ) => {

  const navigate = useNavigate()

  const onPageChange = ( page: number ) => {
    if ( page !== currentPage.page ) {
      return navigate( `/?page=${ page }&size=${ currentPage.size }` )
    }
  }

  const onPageSizeChange = ( _: number, size: number ) => {
    return navigate( `/?page=${ currentPage.page }&size=${ size }` )
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