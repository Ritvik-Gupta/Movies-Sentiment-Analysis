import Button from "@material-ui/core/Button"
import Container from "@material-ui/core/Container"
import { NextPage } from "next"

export interface IIndexProps {}

const Index: NextPage<IIndexProps> = () => {
	return (
		<Container fixed>
			<div>Index Page</div>
			<Button variant='contained' color='primary'>
				Hello World
			</Button>
		</Container>
	)
}

export default Index
