export interface LoginResponse{
  message:string,
  user:User,
  tokens:Token,


}

interface User{
  id:number,
  username:string,
  email:string,
  role:string,
  first_name:string,
  last_name:string,

}

interface Token {
 refresh:string,
 access:string
}
 