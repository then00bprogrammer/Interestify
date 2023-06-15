import React from "react";
import { useEffect, useState } from 'react';
import { useRouter } from "next/router";
import { Box, Flex, Image, Text, Button, Divider, Stack } from "@chakra-ui/react";
import AuthButtons from "./AuthButtons";
import Banner from "./Banner";
import Link from 'next/link';
import { authState } from "@/atoms/userAtom";
import { useRecoilValue } from "recoil";

const Navbar: React.FC = () => {
  const isLoggedIn = useRecoilValue(authState).isLoggedIn;
  const router = useRouter();
  const [scrollPosition, setScrollPosition] = useState(0);
  const [isScrolledPastThreshold, setIsScrolledPastThreshold] = useState(false);
  const isHomePage = router.pathname === '/';

  useEffect(() => {
    const handleScroll = () => {
      const currentPosition = window.pageYOffset;
      setScrollPosition(currentPosition);
      setIsScrolledPastThreshold(currentPosition > 80 + (window.innerHeight * 0.50));
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <Flex
      bg={isHomePage && !isLoggedIn && !isScrolledPastThreshold ? "#ffdf00" : "white"}
      position="fixed"
      width="100vw"
      maxWidth="100vw"
      height="80px"
      padding="10px 10vw"
      zIndex="200"
      justifyContent="space-between"
      alignItems="center"
      overflowX="hidden"
      overflowY="hidden"
    >
      <Link href="/">
        <Text fontWeight="extrabold" fontSize="5xl">
          Interestify
        </Text>

      </Link>
      <Flex>
        <AuthButtons />
      </Flex>
    </Flex>
  );
};


export default Navbar;
