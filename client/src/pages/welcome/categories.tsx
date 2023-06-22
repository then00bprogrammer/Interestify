import React, {useState} from 'react'
import { Stack, InputGroup, InputLeftElement, Input, Icon, Heading } from '@chakra-ui/react'
import AllCategories from '@/components/Category/AllCategories'
import { FaSearch } from 'react-icons/fa'
import { categoriesData } from '@/Handlers/CategoriesData'

const categories = () => {
    const [data,setData] = useState<string[]>(categoriesData);
    const [inputText, setInputText] = useState<string>('');
    
    const getSearchResults = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const searchText = event.target.value;
        setInputText(searchText);
        if (searchText.length < 2) {
          setData(categoriesData);
          return;
        } else {
          try {
            const resp = await fetch('http://127.0.0.1:5000/searchCategory', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                text: searchText,
              }),
            });
    
            const searchResults = await resp.json();
            setData(searchResults);
          } catch (error) {
            console.error(error);
          }
        }
      };
    return (
        <Stack alignItems="center" justifyContent="center">
            <Heading marginTop="5vh" textAlign='center'>SELECT YOUR FAVOURITE CATEGORIES</Heading>
            <InputGroup width="60vw" margin="5vh 5vw 0 5vw">
                <InputLeftElement
                    pointerEvents="none"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    height="100%"
                >
                    <Icon as={FaSearch} />
                </InputLeftElement>
                <Input
                    onChange={getSearchResults}
                    value={inputText}
                    borderRadius={100}
                    height="7vh"
                    borderColor="black"
                    _hover={{ borderColor: "black" }}
                    focusBorderColor="black"
                    type="tel"
                    placeholder="Search Categories"
                />
            </InputGroup>
            <AllCategories filteredData={data}/>
        </Stack>
    )
}

export default categories