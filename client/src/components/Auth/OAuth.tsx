import React from 'react'
import { Stack, Text, Center } from '@chakra-ui/react'
import OauthButtons from './OAuthButtons'

type Props = {
    view: "login" | "signup"
}

const OAuth = ({ view }: Props) => {
    return (
        <>
            <Center>
                <Stack width={['100vw','100vw','100vw','50vw']} padding="20vh 10vw 10vh 10vw"
                paddingTop={['5vh','5vh','5vh','20vh']} paddingBottom={['0','0','0','10vh']}
                >
                    <Text textAlign='center' color="white" fontSize={['5xl','6xl','6xl','6xl']} marginBottom="5vh">{view === "login" ? "Log In" : "Sign Up"}</Text>
                    <OauthButtons imageSrc='https://img.icons8.com/color/48/google-logo.png' providerName='Google' />
                    <OauthButtons imageSrc='https://img.icons8.com/fluency/240/facebook-new.png' providerName='Facebook' />
                </Stack>
            </Center>
        </>
    )
}

export default OAuth