import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { Button, Tooltip } from "antd"

interface Props {
  liked: boolean
  scheduled: boolean
}

export const ScheduledButton = ( {
  liked,
  scheduled
}: Props ) => {

  const ScheduledIcon = () => scheduled ? (
    <CheckCircleOutlined className="liked" />
  ) : (
    <CloseCircleOutlined className="not-liked" />
  )

  return liked ? null : (
    <Tooltip title={ scheduled === true ? "Scheduled" : "Not scheduled" }>
      <Button
        className="no-pad"
        icon={ <ScheduledIcon /> }
        type="text" />
    </Tooltip>
  )
}