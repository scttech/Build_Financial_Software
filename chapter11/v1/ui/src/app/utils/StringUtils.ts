export function stripSubnet(ipWithSubnet: string): string {
  // Split the IP address and subnet mask by the '/' character
  const [ip, subnet] = ipWithSubnet.split('/');

  if (subnet === '32' ) {
    return ip;
  } else {
    return ipWithSubnet;
  }

}