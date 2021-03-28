import CssBaseline from "@material-ui/core/CssBaseline"
import { ThemeProvider } from "@material-ui/core/styles"
import { NextPage } from "next"
import { AppProps } from "next/app"
import Head from "next/head"
import { Fragment, useEffect } from "react"
import { theme } from "../src/theme"

const CustomApp: NextPage<AppProps> = ({ Component, pageProps }) => {
	useEffect(() => {
		const jssStyles = document.querySelector("#jss-server-side")
		jssStyles?.parentElement?.removeChild(jssStyles)
	}, [])

	return (
		<Fragment>
			<Head>
				<title>My page</title>
				<meta name='viewport' content='minimum-scale=1, initial-scale=1, width=device-width' />
			</Head>
			<ThemeProvider theme={theme}>
				<CssBaseline />
				<Component {...pageProps} />
			</ThemeProvider>
		</Fragment>
	)
}

export default CustomApp
