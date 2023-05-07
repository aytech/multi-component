import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { Button, Tooltip } from "antd"

interface Props {
  liked: boolean
  onClick: () => void
}

export const LikedButton = ( {
  liked,
  onClick
}: Props ) => {

  const LikedIcon = () => liked ? (
    <CheckCircleOutlined className="liked" />
  ) : (
    <CloseCircleOutlined className="not-liked" />
  )

  return (
    <Tooltip title={ liked === true ? "Liked" : "Not liked" }>
      <Button
        className="no-pad"
        icon={ <LikedIcon /> }
        onClick={ onClick }
        type="text" />
    </Tooltip>
  )
}