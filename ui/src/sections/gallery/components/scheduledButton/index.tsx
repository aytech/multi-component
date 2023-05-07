import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons"
import { Button, Tooltip } from "antd"

interface Props {
  onClick: () => void
  scheduled: boolean
}

export const ScheduledButton = ( {
  onClick,
  scheduled
}: Props ) => {

  const ScheduledIcon = () => scheduled ? (
    <CheckCircleOutlined className="liked" />
  ) : (
    <CloseCircleOutlined className="not-liked" />
  )

  return (
    <Tooltip title={ scheduled === true ? "Scheduled" : "Not scheduled" }>
      <Button
        className="no-pad"
        icon={ <ScheduledIcon /> }
        onClick={ onClick }
        type="text" />
    </Tooltip>
  )
}