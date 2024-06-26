import React, { ReactElement } from 'react';
import { Flex } from '@chakra-ui/react';
import OAuth from '@/components/Auth/OAuth';
import AuthDivider from '@/components/Auth/AuthDivider';
import LoginForm from '@/components/Auth/LoginForm';
import Head from 'next/head';

const Login = () => {
  return (
    <>
      <Head>
        <title>Interestify - Login</title>
      </Head>

      <Flex flexDirection={['column', 'column', 'column', 'row']} minHeight='100vh' justifyContent="center" bgImage="/assets/auth_bg.avif" backgroundSize='cover'>
        <OAuth view="login"></OAuth>
        <AuthDivider></AuthDivider>
        <LoginForm></LoginForm>
      </Flex>
    </>
  );
};

Login.getLayout = function getLayout(page: ReactElement) {
  return (
    <>
      {page}
    </>
  )
}

export default Login;
