import { DeleteOutlined, DislikeOutlined, LikeOutlined, StopOutlined } from "@ant-design/icons"
import { Button, Col, Tooltip } from "antd"

interface Props {
  dislike: () => void
  disliking: boolean
  hide: () => void
  hiding: boolean
  like: () => void
  liking: boolean
}

export const Actions = ( {
  dislike,
  disliking,
  hide,
  hiding,
  like,
  liking
}: Props ) => {
  return (
    <>
      <Col className="text-center" xs={ disliking || hiding ? 6 : liking ? 12 : 8 }>
        <Button
          className="btn-green"
          loading={ liking }
          onClick={ like }
          type="primary">
          <Tooltip title="Like">
            <LikeOutlined />
          </Tooltip>
        </Button>
      </Col>
      <Col className="text-center" xs={ liking || hiding ? 6 : disliking ? 12 : 8 }>
        <Button
          loading={ disliking }
          onClick={ dislike }
          type="primary">
          <Tooltip title="Dislike">
            <DislikeOutlined />
          </Tooltip>
        </Button>
      </Col>
      <Col className="text-center" xs={ liking || disliking ? 6 : hiding ? 12 : 8 }>
        <Button
          danger
          loading={ hiding }
          onClick={ hide }
          type="primary">
          <Tooltip title="Hide">
            <StopOutlined />
          </Tooltip>
        </Button>
      </Col>
    </>
  )
}