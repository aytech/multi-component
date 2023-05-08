import { DislikeOutlined, LikeOutlined, StopOutlined } from "@ant-design/icons"
import { Button, Col, Tooltip } from "antd"

interface Props {
  dislike: () => void
  disliking: boolean
  hide: () => void
  hiding: boolean
  like: () => void
  liked: boolean
  liking: boolean
  scheduled: boolean
}

export const Actions = ( {
  dislike,
  disliking,
  hide,
  hiding,
  like,
  liked,
  liking,
  scheduled
}: Props ) => {
  return (
    <>
      <Col className="text-center" xs={ disliking || hiding ? 6 : liking ? 12 : 8 }>
        <Button
          className="btn-green"
          disabled={ scheduled }
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
          disabled={ liked }
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