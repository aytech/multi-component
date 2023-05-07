import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { Button, Tooltip } from "antd"

interface Props {
  liked: boolean
}

export const LikedButton = ( {
  liked
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
        type="text" />
    </Tooltip>
  )
}